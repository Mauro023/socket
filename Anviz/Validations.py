import ModelsDB as Eloquent


def update_entrance(request: dict) -> None:
    lastattendance = Eloquent.last_attendance(request['employe_id'], request['workday'])
    attendanceexists = Eloquent.attendance_exists(request['workday'], request['aentry_time'], request['employe_id'])
    employe_exists = Eloquent.employe_exists(request['employe_id'])
    if request['action'] == 128:
        if employe_exists:
            if attendanceexists:
                return print('Este usuario ya registro una entrada.')
            else:
                if lastattendance is None:
                    Eloquent.attendance_repository(request)
                elif request['adeparture_time'] is not None:
                    Eloquent.attendance_repository(request)
                else:
                    return print('Este usuario ya registró una entrada y no ha generado una salida.')
        else:
            return print('Empleado no encontrado')
    elif request['action'] == 129:
        entryDate = request['workday']
        entryTime = request['aentry_time']
        findAttendanceByDay = Eloquent.find_attendance_by_day(entryDate, request['employe_id'])
        if findAttendanceByDay and findAttendanceByDay[2] <= entryTime:
            send_record = list(findAttendanceByDay)
            send_record[3] = entryTime
            Eloquent.update_attendance_by_day(send_record)
        if findAttendanceByDay is None:
            findAttendanceByPreviousDay = Eloquent.find_attendance_by_previous_day(request['employe_id'],
                                                                                   entryDate, entryTime)
            if findAttendanceByPreviousDay is None:
                return print('No se encontró ninguna entrada para el usuario en la fecha especificada.')
            elif findAttendanceByPreviousDay[3] is not None:
                return print('Este usuario ya registró una salida.')
            else:
                finally_record = list(findAttendanceByPreviousDay)
                finally_record[3] = entryTime
                Eloquent.update_attendance_by_day(finally_record)
    else:
        return print('Attendance saved successfully')

