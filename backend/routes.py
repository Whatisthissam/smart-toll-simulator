from flask import Blueprint, request, jsonify
from services import (
    detect_vehicle_service, process_payment_service, manual_payment_service,
    retry_payment_service, simulate_failure_service, get_dashboard_data,
    get_transactions, get_vehicles, get_logs, get_analytics
)

api_bp = Blueprint('api', __name__)

@api_bp.route('/vehicle/detect', methods=['POST'])
def detect_vehicle():
    data = request.json
    result = detect_vehicle_service(data)
    return jsonify(result), result.get('status_code', 200)

@api_bp.route('/payment/process', methods=['POST'])
def process_payment():
    data = request.json
    result = process_payment_service(data)
    return jsonify(result), result.get('status_code', 200)

@api_bp.route('/payment/manual', methods=['POST'])
def manual_payment():
    data = request.json
    result = manual_payment_service(data)
    return jsonify(result), result.get('status_code', 200)

@api_bp.route('/payment/retry', methods=['POST'])
def retry_payment():
    data = request.json
    result = retry_payment_service(data)
    return jsonify(result), result.get('status_code', 200)

@api_bp.route('/failure/simulate', methods=['POST'])
def simulate_failure():
    data = request.json
    result = simulate_failure_service(data)
    return jsonify(result), result.get('status_code', 200)

@api_bp.route('/transactions', methods=['GET'])
def get_transactions_route():
    result = get_transactions(request.args)
    return jsonify(result)

@api_bp.route('/vehicles', methods=['GET'])
def get_vehicles_route():
    result = get_vehicles()
    return jsonify(result)

@api_bp.route('/dashboard', methods=['GET'])
def get_dashboard_route():
    result = get_dashboard_data()
    return jsonify(result)

@api_bp.route('/analytics', methods=['GET'])
def get_analytics_route():
    result = get_analytics()
    return jsonify(result)

@api_bp.route('/logs', methods=['GET'])
def get_logs_route():
    result = get_logs()
    return jsonify(result)
