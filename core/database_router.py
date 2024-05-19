class DatabaseRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    https://docs.djangoproject.com/en/5.0/topics/db/multi-db/
    """

    # Here we only need to route logs app to logs_db
    route_app_labels = {"logs"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read.
        """
        if model._meta.app_label in self.route_app_labels:
            return "logs_db"
        return "default"

    def db_for_write(self, model, **hints):
        """
        Attempts to write.
        """
        if model._meta.app_label in self.route_app_labels:
            return "logs_db"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            return db == "logs_db"
        return "default"
