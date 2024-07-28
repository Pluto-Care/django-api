# Doctor will be able to modify and delete notes that are created by them.
CREATE_DOCTOR_NOTES = dict(id='create:doctor_notes',
                           name='Create doctor notes')

# Permission to delete doctor notes by others.
DELETE_DOCTOR_NOTES = dict(id='delete:doctor_notes',
                           name='Delete doctor notes')

# Permission to view doctor notes by others.
VIEW_DOCTOR_NOTES = dict(id='view:doctor_notes',
                            name='View doctor notes')


base_permission = dict(
    CREATE_DOCTOR_NOTES=CREATE_DOCTOR_NOTES,
    DELETE_DOCTOR_NOTES=DELETE_DOCTOR_NOTES,
    VIEW_DOCTOR_NOTES=VIEW_DOCTOR_NOTES
)
