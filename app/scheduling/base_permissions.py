MODIFY_ALL_APPOINTMENTS = dict(id="modify:appointments",
                               name="Modify Appointments")
VIEW_ALL_APPOINTMENTS = dict(id="view:appointments", name="View Appointments")
MODIFY_ALL_AVAILABILITIES = dict(id="modify:all_availabilities",
                                 name="Modify All Availabilities")
VIEW_ALL_AVAILABILITIES = dict(id="view:all_availabilities",
                               name="View All Availabilities")
MODIFY_ALL_BREAKS = dict(id="modify:all_breaks", name="Modify All Breaks")
VIEW_ALL_BREAKS = dict(id="view:all_breaks", name="View All Breaks")
MODIFY_ALL_LEAVES = dict(id="modify:all_leaves", name="Modify All Leaves")
VIEW_ALL_LEAVES = dict(id="view:all_leaves", name="View All Leaves")

base_permission = dict(
    MODIFY_ALL_APPOINTMENTS=MODIFY_ALL_APPOINTMENTS,
    VIEW_ALL_APPOINTMENTS=VIEW_ALL_APPOINTMENTS,
    MODIFY_ALL_AVAILABILITIES=MODIFY_ALL_AVAILABILITIES,
    VIEW_ALL_AVAILABILITIES=VIEW_ALL_AVAILABILITIES,
    MODIFY_ALL_BREAKS=MODIFY_ALL_BREAKS,
    VIEW_ALL_BREAKS=VIEW_ALL_BREAKS,
)
