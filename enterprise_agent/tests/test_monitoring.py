from enterprise_agent.monitoring import AgentMetrics

import time


metrics = AgentMetrics()


# Request 1
start = metrics.start_request()

time.sleep(0.5)

metrics.record_success(start)


# Request 2
start = metrics.start_request()

time.sleep(0.2)

metrics.record_success(start)


# Request 3
start = metrics.start_request()

time.sleep(0.1)

metrics.record_failure(start)


# ==========================================
# Monitoring Report
# ==========================================

print("\n===== MONITORING REPORT =====")

print(metrics.report())