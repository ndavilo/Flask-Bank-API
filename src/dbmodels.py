import datetime
from random import randint
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email, password):
        """Generates a unique identifier for the User object."""
        is_id_exist = True
        while is_id_exist:
            id = secrets.token_hex(16)
            is_id_exist = User.query.filter_by(id=id).first() is not None

        self.id = id
        self.username = username
        self.password=password
        self.email=email
        
    def __repr__(self):
        return '<User %r>' % self.username


class Customer(db.Model):
    """
            The Customer class has attributes that map to columns in the Customer table, including:
        - `id`: primary key for the Customer table
        - `first_name`: first name of the customer
        - `middle_name`: middle name of the customer
        - `last_name`: last name of the customer
        - `phone_number`: phone number of the customer
        - `email`: email address of the customer
        - `address`: address of the customer
        - `deleted`: a boolean flag indicating whether the customer has been deleted
        - `accounts`: a relationship to the Account table, allowing access to all accounts associated with the customer
    """
    id = db.Column(db.String(32), primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32), nullable=True)
    last_name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    address = db.Column(db.String(32), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    accounts = db.relationship(
        'Account', backref='customer_accounts', lazy=True)


    def __init__(self):
        """Generates a unique identifier for the Customer object."""
        is_id_exist = True
        while is_id_exist:
            id = secrets.token_hex(16)
            is_id_exist = Customer.query.filter_by(id=id).first() is not None

        self.id = id
        
        
    def __repr__(self):
        return '<Customer {}>'.format(self.email)



class Withdraw(db.Model):
    """Model for the Withdraw class

    Attributes:
        amount (float): The amount of the withdrawal
        date (datetime): The date and time of the withdrawal
        account_id (str): The id of the account from which the withdrawal was made
        id (str): The unique identifier for the withdrawal
    """
    amount = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    account_id = db.Column(db.String(32), db.ForeignKey(
        'account.id'), nullable=False)
    id = db.Column(db.String(32), primary_key=True, unique=True)

    def __init__(self):
        """Initialize the Withdraw instance with a unique id

        Generates a unique id using secrets.token_hex(16) and sets it as the 'id' attribute.
        """
        is_id_exist = True
        while is_id_exist:
            id = secrets.token_hex(16)
            is_id_exist = Withdraw.query.filter_by(id=id).first() is not None

        self.id = id

    def __repr__(self):
        """Return a string representation of the Withdraw instance

        Returns:
            str: The string representation of the Withdraw instance, with the format 'Withdraw: {id}'
        """
        return 'Withdraw: {}'.format(self.id)


class Deposit(db.Model):
    """Class representing the deposit model

    This class defines the structure of a deposit in the database and includes methods for generating a unique identifier for the deposit.

    Args:
        db (SQLAlchemy Object): The SQLAlchemy object to associate the model with

    Attributes:
        amount (float): The amount of the deposit
        date (datetime): The date of the deposit
        account (str): The id of the account associated with the deposit
        id (str): The unique identifier of the deposit
    """
    amount = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    account = db.Column(db.String(32), db.ForeignKey(
        'account.id'), nullable=False)
    id = db.Column(db.String(32), primary_key=True, unique=True)

    def __init__(self):
        """Generates a unique identifier for the deposit object."""
        is_id_exist = True
        while is_id_exist:
            id = secrets.token_hex(16)
            is_id_exist = Deposit.query.filter_by(id=id).first() is not None

        self.id = id

    def __repr__(self):
        """Returns a string representation of the deposit object."""
        return 'Deposit: {}'.format(self.id)


class Transfer(db.Model):
    """This class represents the Transfer model for a bank transfer between two accounts.

    Args:
        db (sqlalchemy.ext.declarative.api.DeclarativeMeta): The SQLAlchemy class from which to inherit.
    """
    debit = db.Column(db.String(32), db.ForeignKey(
        'account.id'), nullable=False)
    credit = db.Column(db.String(32), db.ForeignKey(
        'account.id'), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id = db.Column(db.String(32), primary_key=True, unique=True)
    
    debit_account = db.relationship("Account", foreign_keys=[debit], back_populates="debit_transfers")
    credit_account = db.relationship("Account", foreign_keys=[credit], back_populates="credit_transfers")

    def __init__(self):
        """The constructor method for the Transfer class.

        Generates a unique id for the transfer.
        """
        is_id_exist = True
        while is_id_exist:
            id = secrets.token_hex(16)
            is_id_exist = Transfer.query.filter_by(id=id).first() is not None

        self.id = id

    def __repr__(self):
        """Returns a string representation of the Transfer object."""
        return 'Transfer: {}'.format(self.id)


class AppUser(db.Model):
    """The `AppUser` model represents a user of the application.

    Args:
        db (sqlalchemy.ext.declarative.api.DeclarativeMeta): The SQLAlchemy class that is being used as a base for creating the model.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True,
                   comment="The unique identifier for the user.")
    account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False,
                        comment="The unique identifier of the account associated with this user.")
    password = db.Column(db.String(32), unique=True, nullable=False,
                         comment="The password for the user's account.")
    varified = db.Column(db.Boolean, unique=True, default=False,
                         comment="Whether the user's account has been verified.")

    def __repr__(self) -> str:
        return 'AppUser: {}'.format(self.account)


class AppOTP(db.Model):
    """Model class representing OTP in the Application.

    Args:
        db (SQLAlchemy): An instance of SQLAlchemy.

    Attributes:
        id (db.Column): A string column representing the unique identifier of the OTP.
        dateTime (db.Column): A datetime column representing the time the OTP was created.
        closed (db.Column): A boolean column representing the status of the OTP (if it has been used or not).
        account (db.Column): An integer column representing the account associated with the OTP.
    """
    id = db.Column(db.String(32), primary_key=True, unique=True)
    dateTime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    closed = db.Column(db.Boolean, unique=True, default=False)
    account = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    def __init__(self, id):
        """Initializes the OTP.

        Creates a unique identifier for the OTP.

        Args:
            id (int): An optional argument to specify the identifier of the OTP.
                      If not provided, a unique identifier will be created.
        """
        super().__init__(self)
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = randint(100000, 1000000)
                is_id_exist = AppOTP.objects.filter(id=id).exists()

            self.id = id

    def __repr__(self) -> str:
        return 'AppOTP: {}'.format(self.account)


class Account(db.Model):
    """_summary_

    Args:
        The Account class has attributes that map to columns in the Account table, including:
        - `customer_id`: foreign key to the Customer table, indicating the customer associated with this account
        - `withdraw_account`: a relationship to the Withdraw table, allowing access to all withdraw transactions associated with this account
        - `deposit_account`: a relationship to the Deposit table, allowing access to all deposit transactions associated with this account
        - `transfer_id`: a relationship to the Transfer table, allowing access to all transfer transactions associated with this account
        - `app_user_id`: a relationship to the AppUser table, allowing access to the AppUser associated with this account
        - `app_otp_id`: a relationship to the AppOTP table, allowing access to the AppOTP associated with this account
        - `account_type`: the type of the account, defaults to 'Savings'
        - `balance`: the balance of the account, defaults to 0.0
        - `date`: the date the account was created, defaults to the current UTC time
        - `transaction_key`: a transaction key associated with the account, used for security
        - `flag`: a boolean flag, used for security
        - `closed`: a boolean flag indicating whether the account is closed, defaults to False
        - `id`: primary key and unique identifier for the account


    Returns:
        _type_: _description_
    """
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    withdraw_account = db.relationship(
        'Withdraw', backref='withdraw_account', lazy=True)
    deposit_account = db.relationship(
        'Deposit', backref='deposit_account', lazy=True)
    debit_transfers = db.relationship("Transfer", foreign_keys=[Transfer.debit], back_populates="debit_account")
    credit_transfers = db.relationship("Transfer", foreign_keys=[Transfer.credit], back_populates="credit_account")
    app_user_id = db.relationship('AppUser', backref='appuser_account', lazy=True)
    app_otp_id = db.relationship('AppOTP', backref='appotp_account', lazy=True)
    account_type = db.Column(db.String(32), default='Savings')
    balance = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    transaction_key = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.Boolean, default=False)
    closed = db.Column(db.Boolean, default=False)
    id = db.Column(db.String(32), primary_key=True, unique=True)

    def __init__(self, id=None):
        """Initialize the Account instance with a unique id

        Generates a unique id using secrets.token_hex(16) and sets it as the 'id' attribute.
        """
        # if creating a new account
        is_id_exist = True
        while is_id_exist:
            id = secrets.token_hex(16)
            is_id_exist = Account.query.filter_by(id=id).first() is not None

        self.id = id

    def __repr__(self):
        return '<Account {}>'.format(self.id)