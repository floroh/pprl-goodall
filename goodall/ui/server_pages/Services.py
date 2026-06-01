from goodall.api_helper.service_status import get_service_health_checks
import streamlit as st

st.subheader("Service status")
check_mlflow = st.toggle("Include mlflow connection check", value=False)
results = get_service_health_checks(
    check_mlflow=check_mlflow
)

healthy = sum(s.healthy for s in results)
cols = st.columns(3)
cols[0].metric("Total", len(results))
cols[1].metric("Healthy", healthy)
cols[2].metric("Unhealthy", len(results) - healthy)

st.divider()

for s in results:
    icon = "🟢" if s.healthy else "🔴"
    color = "green" if s.healthy else "red"

    with st.container(border=True):
        c1, c2 = st.columns([2, 1])
        c1.write(f"**{icon} {s.name}**")
        c1.code(s.endpoint, language=None)
        c2.markdown(f":{color}[{'**HEALTHY**' if s.healthy else '**UNHEALTHY**'}]")