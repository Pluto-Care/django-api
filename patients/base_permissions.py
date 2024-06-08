VIEW_PATIENTS = dict(id='read:patients', name='View patients')
CREATE_PATIENTS = dict(id='create:patients', name='Create patients')
UPDATE_PATIENTS = dict(id='update:patients', name='Update patients')
DELETE_PATIENTS = dict(id='delete:patients', name='Delete patients')

base_permission = dict(
    VIEW_PATIENTS=VIEW_PATIENTS,
    CREATE_PATIENTS=CREATE_PATIENTS,
    UPDATE_PATIENTS=UPDATE_PATIENTS,
    DELETE_PATIENTS=DELETE_PATIENTS,
)
