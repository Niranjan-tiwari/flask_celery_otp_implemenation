from flask import Flask, request, jsonify
from celery import Celery
from otp_sys import TwoFactor
import time

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def my_background_task(arg1, arg2):
    time.sleep(10)
    result = arg1 + arg2
    return result


@celery.task
def send_otp_to_user(mobile_number):
    otp_obj = TwoFactor(mobile_num=mobile_number)
    response, status = otp_obj.send_opt()
    print(response)  # Todo: Store session id in table
    print(status)
    return status


@celery.task
def verify_otp_of_user(mobile_number, session_id, otp):
    otp_obj = TwoFactor(mobile_num=mobile_number)
    response, status = otp_obj.verify_otp(session_id=session_id, otp=otp)
    print(response)
    print(status)
    return True
    

@app.route('/send_otp', methods=["POST"])
def send_otp():
    response = {
        "success": False,
        "message": ""
    }
    try:
        mobile_number = request.json.get("mobile_number")
        send_otp_to_user.delay(mobile_number)
        response["success"] = True
        response["message"] = "Sending otp to {0}".format(mobile_number)        
    except Exception as ex:
        response["message"] = ex
    return jsonify(response)


@app.route('/verify_otp', methods=["POST", "GET"])
def verify_otp():
    response = {
        "success": False,
        "message": ""
    }
    if request.method == "POST":
        try:
            mobile_number = request.json.get("mobile_number")
            otp = request.json.get("otp")
            session_id = request.json.get("session_id")
            verify_otp_of_user.delay(mobile_number, session_id, otp)
            response["success"] = True
            response["message"] = "verifying otp of {0}".format(mobile_number)        
        except Exception as ex:
            response["message"] = ex
    elif request.method == "GET":
        try:
            mobile_number = request.args.get("mobile_number")
            response["message"] = "number data" + str(mobile_number)
        except Exception as ex:
            response["message"] = ex
    return jsonify(response)


if __name__ == "__main__":
    app.run()
