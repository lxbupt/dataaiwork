# _*_ coding : utf-8 _*_
# @Time : 2024/1/1 14:32
# @Author : 战斧牛排炖洋芋
# @File : ImageDao
# @Project : dataaiwork
from dao.BaseDao import BaseDao


class ImageDao(BaseDao):
    def __init__(self):
        super().__init__()

    def insert_image(self, filename, filepath, classes, possibility, eventtime):
        """
        插入一条图像记录
        """
        sql = """
            INSERT INTO t_images (filename, filepath, classes, possibility, eventtime)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (filename, filepath, classes, possibility, eventtime)

        try:
            self.execute(sql, params)
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            print(f"Error inserting image record: {e}")
            return False

    def get_all_images(self):
        """
        获取所有图像记录
        """
        sql = "SELECT * FROM t_images"

        try:
            self.execute(sql)
            return self.fetchall()
        except Exception as e:
            print(f"Error retrieving all image records: {e}")
            return []

    def get_filepath_by_imagesid(self, imagesid):
        """
        根据 imagesid 查询 filepath
        """
        sql = "SELECT filepath FROM t_images WHERE imagesid = %s"
        params = (imagesid,)

        try:
            self.execute(sql, params)
            result = self.fetchone()
            print(f"Result of the query: {result}")
            return result.get('filepath')
        except Exception as e:
            print(f"Error retrieving filepath by imagesid: {e}")
            return None

    def get_images_by_classes(self, classes):
        """
        根据 classes 查询图像记录
        """
        sql = "SELECT * FROM t_images WHERE classes = %s"
        params = (classes,)

        try:
            self.execute(sql, params)
            return self.fetchall()
        except Exception as e:
            print(f"Error retrieving image records by classes: {e}")
            return []
