MODIFY_APPOINTMENTS = dict(id="modify:appointments",
                           name="Modify Appointments")
MAKE_APPOINTMENTS = dict(id="make:appointments",
                         name="Make Appointments")
VIEW_APPOINTMENTS = dict(id="view:appointments", name="View Appointments")

base_permission = dict(
    MODIFY_APPOINTMENTS=MODIFY_APPOINTMENTS,
    MAKE_APPOINTMENTS=MAKE_APPOINTMENTS,
    VIEW_APPOINTMENTS=VIEW_APPOINTMENTS
)
