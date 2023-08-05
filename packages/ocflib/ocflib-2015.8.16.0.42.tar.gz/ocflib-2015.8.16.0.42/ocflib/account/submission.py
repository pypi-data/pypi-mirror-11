"""New account submission.

The functions here are all Celery tasks that submit new accounts for creation.
Account creation always happens on the admin server (supernova), but new
accounts can be submitted from anywhere (e.g. accounts.ocf.berkeley.edu (atool)
or the approve command-line staff script).

A pre-requisite to using functions in this module is configuring Celery with an
appropriate broker and backend URL (probably Redis).

    from celery import Celery
    from ocflib.account.submission import get_tasks

    celery_app = Celery(broker='..', backend='..')
    tasks = get_tasks(celery_app)

    result = tasks.create_account.delay(..)

    # result is now an AsyncResult:
    # https://celery.readthedocs.org/en/latest/reference/celery.result.html#celery.result.AsyncResult
    #
    # You can immediately resolve it with result.wait(timeout=5), or grab
    # result.id and fetch it later.
"""
from collections import namedtuple
from contextlib import contextmanager

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ocflib.account.creation import create_account
from ocflib.account.creation import decrypt_password
from ocflib.account.creation import validate_callink_oid
from ocflib.account.creation import validate_calnet_uid
from ocflib.account.creation import validate_email
from ocflib.account.creation import validate_password
from ocflib.account.creation import validate_username
from ocflib.account.creation import ValidationError
from ocflib.account.creation import ValidationWarning


_AccountSubmissionTasks = namedtuple('AccountSubmissionTasks', [
    'create_account',
])


class AccountCreationCredentials(namedtuple('AccountCreationCredentials', [
    'encryption_key',
    'mysql_uri',
    'kerberos_keytab',
    'kerberos_principal',
])):
    pass


class NewAccountRequest(namedtuple('NewAccountRequest', [
    'user_name',
    'real_name',
    'is_group',
    'calnet_uid',
    'callink_oid',
    'email',
    'encrypted_password',
    'handle_warnings',
])):
    """Request for account creation.

    :param user_name:
    :param real_name:
    :param is_group:
    :param calnet_uid: uid (or None)
    :param callink_oid: oid (or None)
    :param email:
    :param encrypted_password:
    :param handle_warnings: one of WARNINGS_WARN, WARNINGS_SUBMIT,
                            WARNINGS_CREATE
        WARNINGS_WARN: don't create account, return warnings
        WARNINGS_SUBMIT: don't create account, submit for staff approval
        WARNINGS_CREATE: create the account anyway
    """
    WARNINGS_WARN = 'warn'
    WARNINGS_SUBMIT = 'submit'
    WARNINGS_CREATE = 'create'


Base = declarative_base()


class StoredNewAccountRequest(Base):
    """SQLAlchemy object for holding account requests."""

    __tablename__ = 'request'

    # TODO: enforce these lengths during submission as errors
    id = Column(Integer, primary_key=True)
    user_name = Column(String(255), unique=True, nullable=False)
    real_name = Column(String(255), nullable=False)
    is_group = Column(Boolean, nullable=False)
    calnet_uid = Column(Integer, nullable=True)
    callink_oid = Column(Integer, nullable=True)
    email = Column(String(255), nullable=False)
    encrypted_password = Column(LargeBinary(510), nullable=False)


class NewAccountResponse(namedtuple('NewAccountResponse', [
    'status',
    'errors',
])):
    """Response to an account creation request.

    :param status: one of CREATED, FLAGGED, PENDING, REJECTED
        CREATED: account was created successfully
        FLAGGED: account was flagged and not submitted; the response includes a
                 list of warnings. The user can choose to continue, and should
                 send another request with handle_warnings=WARNINGS_SUBMIT.
        PENDING: account was flagged and submitted; staff will manually review
                 it, and the user will receive an email in a few days
        REJECTED: account cannot be created due to a fatal error (e.g. username
                  already taken)
    :param errors: list of errors (or None)
    """
    CREATED = 'created'
    FLAGGED = 'flagged'
    PENDING = 'pending'
    REJECTED = 'rejected'


def _validate_request(request, credentials):
    """Validate a request, returning lists of errors and warnings."""
    errors, warnings = [], []

    @contextmanager
    def validate_section():
        try:
            yield
        except ValidationWarning as ex:
            warnings.append(str(ex))
        except ValidationError as ex:
            errors.append(str(ex))

    # TODO: figure out where to sanitize real_name
    # TODO: check username against pending requests
    # TODO: check calnet uid / callink oid against pending requests

    with validate_section():
        validate_username(request.user_name, request.real_name)

    with validate_section():
        if request.is_group:
            validate_callink_oid(request.callink_oid)
        else:
            validate_calnet_uid(request.calnet_uid)

    with validate_section():
        validate_email(request.email)

    with validate_section():
        password = decrypt_password(
            request.encrypted_password,
            credentials.encryption_key,
        )
        validate_password(request.user_name, password)

    return errors, warnings


def _submit_account(request, session):
    stored_request = StoredNewAccountRequest(
        user_name=request.user_name,
        real_name=request.real_name,
        is_group=request.is_group,
        calnet_uid=request.calnet_uid,
        callink_oid=request.callink_oid,
        email=request.email,
        encrypted_password=request.encrypted_password,
    )

    # TODO: error handling
    session.add(stored_request)
    session.commit()


def _create_account(request, credentials, report_status):
    create_account(
        user=request.user_name,
        password=decrypt_password(
            request.encrypted_password,
            credentials.encryption_key,
        ),
        real_name=request.real_name,
        email=request.email,
        calnet_uid=request.calnet_uid,
        callink_oid=request.callink_oid,
        keytab=credentials.kerberos_keytab,
        admin_principal=credentials.kerberos_principal,
        report_status=report_status,
    )
    return NewAccountResponse(
        status=NewAccountResponse.CREATED,
        errors=[],
    )


def get_tasks(celery_app, credentials=None):
    """Return Celery tasks instantiated against the provided instance."""

    @celery_app.task
    def create_account(request):
        # status reporting
        status = []

        def report_status(line):
            """Update task status by adding the given line."""
            status.append(line)
            create_account.update_state(
                state='PROGRESS',
                meta={'status': status},
            )

        # mysql, for stored account requests
        Session = None

        def get_session():
            nonlocal Session
            if Session is None:
                Session = sessionmaker(
                    bind=create_engine(credentials.mysql_uri),
                )
            return Session()

        # actual account creation
        CREATE_ACCOUNT, SUBMIT_ACCOUNT = 'create_account', 'submit_account'
        action = CREATE_ACCOUNT

        report_status('Validating account request')
        errors, warnings = _validate_request(request, credentials)
        report_status('Validated account request')

        if errors:
            # Fatal errors which cannot be bypassed, even with staff approval.
            return NewAccountResponse(
                status=NewAccountResponse.REJECTED,
                errors=(errors + warnings),
            )

        if warnings:
            # Non-fatal errors; the frontend can choose to create the account
            # anyway, submit the account for staff approval, or get a response
            # with a list of warnings for further inspection.
            if request.handle_warnings == NewAccountRequest.WARNINGS_CREATE:
                pass
            elif request.handle_warnings == NewAccountRequest.WARNINGS_SUBMIT:
                action = SUBMIT_ACCOUNT
            elif request.handle_warnings == NewAccountRequest.WARNINGS_WARN:
                return NewAccountResponse(
                    status=NewAccountResponse.FLAGGED,
                    errors=warnings,
                )
            else:
                raise ValueError(
                    'Not familiar with handle_warnings={}'.format(
                        request.handle_warnings,
                    ),
                )

        if action == SUBMIT_ACCOUNT:
            report_status('Submitting account for staff approval')
            return _submit_account(request, get_session())
        elif action == CREATE_ACCOUNT:
            return _create_account(request, credentials, report_status)

    return _AccountSubmissionTasks(
        create_account=create_account,
    )
