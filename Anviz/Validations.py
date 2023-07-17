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
                #Eloquent.attendance_repository(request)
                ...
            elif request['adeparture_time'] is not None:
                #Aqui va el mismo insert into
                #Eloquent.attendance_repository(request)
                ...
            else:
                return print('Este usuario ya registró una entrada y no ha generado una salida.')
    elif request['action'] == 129:
        #Siguiente parte de la validación
        #entryDate = request['workday']
        #entryTime = request['aentry_time']
        #findAttendanceByDay = Eloquent.find_attendance_by_day(entryDate, request['employe_id'])
        #if findAttendanceByDay and findAttendanceByDay[2] <= entryTime:
        ...

def prueba():
    aux = Eloquent.find_attendance_by_day('2023-06-15', 12)
    if aux:
        print(aux)
    else:
        print('consulta vacia')
if __name__ == '__main__':
    #print(Eloquent.attendance_exists('2023-05-11', '08:04:00',4))
    #print(Eloquent.last_attendance(12, '2023-05-11'))
    prueba()








