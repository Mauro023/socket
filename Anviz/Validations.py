import ModelsDB as Eloquent

def update_entrance(request: dict) -> None:
    lastattendance = Eloquent.last_attendance(request['employe_id'], request['workday'])
    attendanceexists = Eloquent.attendance_exists(request['workday'], request['aentry_time'], request['employe_id'])
    if request['action'] == 128:
        if attendanceexists:
            return print('Este usuario ya registro una entrada.')
        else:
            if lastattendance:
                #Aqui va el insert into
                ...
            elif request['adeparture_time'] is not None:
                #Aqui va el mismo insert into
                ...
            else:
                return print('Este usuario ya registró una entrada y no ha generado una salida.')
    elif request['action'] == 129:
        ...


if __name__ == '__main__':
    print(Eloquent.last_attendance(12, '2023-04-28'))







