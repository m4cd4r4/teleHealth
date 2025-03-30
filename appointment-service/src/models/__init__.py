# Import models so they are registered with SQLAlchemy
from .appointment import Appointment, AppointmentStatus
from .schedule import Schedule, ScheduleSlot
from .notification import AppointmentNotification, NotificationType
