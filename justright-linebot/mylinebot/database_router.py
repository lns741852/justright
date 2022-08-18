from django.conf import settings

# DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING


class HRCS_test_Router(object):  # 配置HRCS_test的路由，去連線hvdb資料庫
    """
    A router to control all database operations on models in the HRCS_test application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read HRCS_test models go to hvdb DB.
        """
        if model._meta.app_label == 'HRCS_test':  # app name（如果該app不存在，則無法同步成功）
            return 'HRCS_test'  # hvdb為settings中配置的database節點名稱，並非db name。dbname為testdjango
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write HRCS_test models go to hvdb DB.
        """
        if model._meta.app_label == 'HRCS_test':
            return 'HRCS_test'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the HRCS_test app is involved.
        當 obj1 和 obj2 之間允許有關係時返回 True ，不允許時返回 False ，或者沒有 意見時返回 None 。
        """
        if obj1._meta.app_label == 'HRCS_test' or \
                obj2._meta.app_label == 'HRCS_test':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the HRCS_test app only appears in the hvdb database.
        """
        if db == 'HRCS_test':
            return app_label == 'HRCS_test'
        elif app_label == 'HRCS_test':
            return False

    def allow_syncdb(self, db, model):  # 決定 model 是否可以和 db 為別名的資料庫同步
        if db == 'HRCS_test' or model._meta.app_label == "HRCS_test":
            return False  # we're not using syncdb on our hvdb database
        else:  # but all other models/databases are fine
            return True
        return None
