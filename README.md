
# AfroSec-Analytics
**SentinelPay: Real-Time Fraud Detection and Response**

---

## PROJECT DESCRIPTION

The project aims to detect fraudulent activities in transaction data using anomaly detection models like Isolation Forest and One-Class SVM, alongside supervised models for comparison.

Key steps include data preprocessing, model evaluation, and developing a real-time monitoring system to detect and respond to suspicious transactions. The system will classify anomalies, freeze affected accounts, and escalate unresolved cases for human review.

Additionally, we are considering utilizing an HTML webpage connected to a database, where AI capabilities, such as transfer learning, will assist with continuous monitoring and improve the model’s performance over time.

---

## FACULTY ADVISOR AGREEMENT

I, Dr. Mahmoud Abdelsalam, have agreed to be the faculty advisor for the project team listed below. This includes meeting with the students at least 7 times during the semester during my office hours or other times at my convenience.

I will give technical advice, encouragement, and make sure that the project stays within the scope of a one semester senior project. I am not expected to design or implement code but will read and give comments to related course documents (Requirements, Specification, Design, and Final Documentation). Furthermore, I agree that the project described above is an appropriate project (if not, have the project team to revise it to your satisfaction).

---

## 🧪 How to Run SentinelPay (Frontend + Backend)

### 📦 Backend (Gradio AI Fraud Detection)

1. Open terminal and navigate to the backend folder:

```powershell
cd "C:\Users\bgbry\OneDrive\Documents\COMP 496\New\fraud-model2"
```

2. Build the Docker container:

```powershell
docker build -t fraud-api .
```

✅ You should see:

```
[+] Building ... FINISHED
=> naming to docker.io/library/fraud-api:latest
```

3. Run the container (interactive, shows Gradio output):

```powershell
docker run -it -p 7860:7860 fraud-api
```

✅ You should see:

```
* Running on local URL:  http://0.0.0.0:7860
```

Leave this terminal open while running the site.

---

### 🌐 Frontend (Dashboard Site)

1. Open the `AfroSec-Analytics` folder in **VS Code**.
2. Right-click on `About.html` → **Open with Live Server**
3. Your browser will open to:

```
http://127.0.0.1:5500/About.html
```

4. Click the **SentinelPay 🔔** link in the sidebar.

✅ It will check if the backend is running and open `http://localhost:7860` in a new tab.

---

### 🛠 SentinelPay Link JS

The `SentinelPay` sidebar link includes smart JS:

```html
<a href="#" onclick="checkAndOpenSentinelPay(event)" target="_blank"><i>🔔</i>SentinelPay</a>

<script>
function checkAndOpenSentinelPay(event) {
    event.preventDefault();
    fetch("http://localhost:7860/", { mode: "no-cors" })
        .then(() => window.open("http://localhost:7860/", "_blank"))
        .catch(() => alert("SentinelPay is not running. Please start the backend."));
}
</script>
```

---

Let me know if you'd like a downloadable `.bat` or `.sh` file to auto-run everything in one click.
