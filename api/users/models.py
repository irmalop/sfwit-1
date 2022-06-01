from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class  UserManager(BaseUserManager):
    """Manager para usuarios"""
    def create_user(self,email, password=None):
        """Crear nuevo user"""
        if email is None:
            raise TypeError('Users should have a email')
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    """Modelo base de datos para usuario en el sistema"""
    email = models.EmailField(max_length=100, verbose_name='Correo', unique=True)
    is_applicant = models.BooleanField('applicant status', default=False)
    is_employer = models.BooleanField('employer status', default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
 
    def __str__(self):
        return self.email
    def tokens_refresh(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)
    def tokens_access(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)            
        

    class Meta:
        db_table='users'
        ordering = ['email']

# default values that can be overriden in settings.py
FLB_MAX_FAILURES = 3
FLB_BLOCK_INTERVAL = 5
# FLB_LOCK_DURATION = int( getattr( settings, 'FLB_LOCK_DURATION', 10 ) )


class FailedAttempt( models.Model ):
    email = models.EmailField( 'Email', max_length=255 )
    failures = models.PositiveIntegerField( 'Failures', default=0 )
    timestamp = models.DateTimeField( 'Last failed attempt', auto_now=True )

    def too_many_failures( self ):
        """ 
        Check if the minimum number of failures needed for a block
        has been reached 
        """
        return self.failures >= FLB_MAX_FAILURES

    def recent_failure( self ):
        """
        Checks if the timestamp one the FailedAttempt object is
        recent enough to result in an increase in failures
        """
        return datetime.now( ) < self.timestamp + timedelta( \
               minutes=FLB_BLOCK_INTERVAL )

    def blocked( self ):
        """ 
        Shortcut function for checking both too_many_failures 
        and recent_failure 
        """
        return self.too_many_failures( ) and self.recent_failure( )
    blocked.boolean = True


    # def unblocked( self ):
    #     """
    #     Checks if the lock duration is
    #     antique enough to result in an unblock
    #     """
    #     return datetime.now( ) >  self.timestamp + timedelta( \
    #            minutes=FLB_LOCK_DURATION )
    # blocked.boolean = False

    def __unicode__(self):
        return u'%s (%d failures until %s): ' % \
               ( self.email,self.failures, self.timestamp )

    class Meta:
        ordering = [ '-timestamp' ]