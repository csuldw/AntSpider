#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:03:02 2019
将movie中的actor_ids和director_ids转存到person_obj表中
@author: liudiwei
"""

import database as db
cursor = db.connection.cursor()

if __name__ == "__main__":

    sql = "SELECT distinct(actor_ids),director_ids FROM movies"
    cursor.execute(sql)
    all_person = cursor.fetchall()

    person_ids = []
    for person_item in all_person:
        actor_list = person_item["actor_ids"].split("|")
        director_list = person_item["director_ids"].split("|")
        actor_list.extend(director_list)
        
        for actor_info in actor_list:
            if ":" not in actor_info:
                continue
            name = actor_info.split(":")[0].replace("\"", "")
            person_id = actor_info.split(":")[1]
            if person_id in person_ids:
                continue
            
            if person_id == "":
                continue
            columns = ["person_id", "name"]
            fields = ",".join(columns)
            sql = 'INSERT INTO person_obj(%s) VALUES ("%s","%s")' % (fields, person_id, name)
            print(sql)
            cursor.execute(sql)
            db.connection.commit()
            person_ids.append(person_id)
