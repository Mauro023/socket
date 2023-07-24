import ModelsPyodbc as Eloquent


def update_entrance(request: dict) -> None:
    lastattendance = Eloquent.last_attendance(request['employe_id'], request['workday'], request['aentry_time'])
    attendanceexists = Eloquent.attendance_exists(request['workday'], request['aentry_time'], request['employe_id'])
    employe_exists = Eloquent.employe_exists(request['employe_id'])
    if employe_exists:
        if attendanceexists:
            return print('Este usuario ya registro una entrada.')
        else:
            if lastattendance is None:
                Eloquent.attendance_repository(request)
            elif lastattendance[3] is not None:
                Eloquent.attendance_repository(request)
            else:
                return print('Este usuario ya registró una entrada y no ha generado una salida.')
    else:
        return print('Empleado no encontrado')


def update_output(request: dict) -> None:
    entryDate = request['workday']
    entryTime = request['aentry_time']
    #Se captura la asistencia del día actual
    findAttendanceByDay = Eloquent.find_attendance_by_day(entryDate, request['employe_id'])
    if findAttendanceByDay:
        if findAttendanceByDay and findAttendanceByDay[2] <= entryTime:
            send_record = list(findAttendanceByDay)
            send_record[3] = entryTime
            Eloquent.update_attendance_by_day(send_record)

    elif findAttendanceByDay is None:
        findAttendanceByPreviousDay = Eloquent.find_attendance_by_previous_day(request['employe_id'], entryDate, entryTime)
        print(findAttendanceByPreviousDay)
        if findAttendanceByPreviousDay is None:
            return print('No se encontró ninguna entrada para el usuario en la fecha especificada.')
        else:
            finally_record = list(findAttendanceByPreviousDay)
            finally_record[3] = entryTime
            Eloquent.update_attendance_by_day(finally_record)


def prueba():
    data = {
        "workday": '2023-07-24',
        "aentry_time": '17:00:00',
        "adeparture_time": None,
        "employe_id": 38,
        "action": 128,
    }
    #update_entrance(data)
    #update_output(data)
    print(Eloquent.find_attendance_by_day('12:00:00', 38))

if __name__ == '__main__':
    #print(Eloquent.attendance_exists('2023-05-11', '08:04:00',4))
    #print(Eloquent.last_attendance(12, '2023-05-11'))
    prueba()








