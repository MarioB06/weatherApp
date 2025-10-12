# WetterApp – DevOps Projekt (Modul 324)

## 1. Projektstart und Zielsetzung
- **Ziel:** Eine CI/CD-Pipeline für das WetterApp-Projekt aufbauen, die Build, Tests und Deployment automatisiert.
- **Teamaufteilung:**  
  Zu Beginn arbeiteten Mario und Luan gemeinsam an der Infrastruktur (VM, Netzwerke, Sicherheit).  
  Nach der grundlegenden VM-Einrichtung trennten sich die Aufgaben – Mario betreute weiterhin Infrastruktur und Sicherheit, während Luan sich auf Jenkins, Docker und die Pipeline konzentrierte.  
  Entscheidungen wurden gemeinsam getroffen.

---

## 2. Vorbereitung der virtuellen Maschine
1. **VM-Auswahl**
   - Ubuntu-Server-VM in der Private-Cloud.
   - Spezifikationen: 4 vCPUs, 8 GB RAM, 100 GB SSD.

2. **Erste Stolpersteine**
   - Das vorinstallierte Image war veraltet, wodurch `apt update` regelmäßig fehlschlug.  
   - **Lösung:** Neues Cloud-Image genutzt und direkt nach dem ersten Boot aktualisiert (`apt update && apt upgrade`).

3. **Netzwerk & Zugriff**
   - SSH war anfangs blockiert, da die Standard-Sicherheitsgruppe nur internen Traffic zuließ.  
   - **Lösung:** Firewall-Regeln angepasst (Port 22/tcp freigegeben) und Fail2ban aktiviert.

4. **Nutzer- und Rechteverwaltung**
   - Gemeinsamer Benutzer `ci-admin` angelegt.  
   - SSH-Keys hinterlegt, Passwort-Login deaktiviert.

---

## 3. Basis-Setup auf der VM
1. **Systempakete**
   - Installation von Docker, Docker Compose und Git.  
   - Problem: Docker startete nach einem Reboot nicht automatisch.  
   - **Lösung:** `systemctl enable docker` und Logs geprüft (`journalctl -u docker`).

2. **Python- und Node-Umgebung**
   - Getrennte Umgebungen für Backend (Python) und Frontend (Node).  
   - Nutzung von `pyenv` und `nvm` zur sauberen Versionsverwaltung.

3. **Monitoring & Logging**
   - Tools wie `htop`, `iotop` und `docker stats` installiert.  
   - SSH-Logins über `journalctl -u ssh` überwacht.

---

## 4. Jenkins-Installation und -Konfiguration
> **Ab hier arbeiteten wir getrennt weiter:**  
> Mario fokussierte sich auf Infrastrukturpflege, während Luan die Jenkins-Umgebung und Pipeline implementierte.

1. **Installationsprobleme**
   - Fehlende Java-Abhängigkeiten (`OpenJDK 11`).  
   - **Lösung:** `apt install openjdk-11-jdk` vor Jenkins-Installation.

2. **Jenkins als Dienst**
   - Jenkins startete zunächst, stoppte aber nach kurzer Zeit mit Speicherfehlern.  
   - **Ursache:** Zu kleiner Heap (256 MB).  
   - **Lösung:** `JAVA_OPTS="-Xms512m -Xmx2048m"` in `/etc/default/jenkins` angepasst.

3. **Reverse Proxy & TLS**
   - Nginx als Proxy vorgeschaltet.  
   - HTTPS über Let’s Encrypt (`certbot`) eingerichtet.

4. **Benutzer- und Rechteverwaltung**
   - Neues Admin-Konto angelegt.  
   - Matrix-Sicherheit aktiviert, nur unser Team darf Pipelines bearbeiten.

---

## 5. Pipeline-Aufbau
1. **Repository-Anbindung**
   - Jenkins mit GitHub-Webhooks verbunden.  
   - Problem: Webhook-Requests wurden vom Proxy blockiert (`X-Forwarded-Proto` fehlte).  
   - **Lösung:** Nginx-Konfiguration angepasst und Jenkins neu gestartet.

2. **Build-Stufen**
   - **Backend:** Python-Tests via `pytest`, statische Analyse mit `flake8`.  
   - **Frontend:** `npm install`, `npm run build`, `npm run test`.  
   - **Docker:** Multi-Stage Builds, Push in interne Registry.

3. **Credentials-Handling**
   - Secrets (Registry-Token, GitHub PAT) im Jenkins-Credentials-Store.  
   - Projektbezogene Credentials für die Pipeline eingerichtet.

4. **Automatisiertes Deployment**
   - Nach erfolgreichem Build → `docker-compose pull && docker-compose up -d`.  
   - Rolling-Restart sorgt für minimale Downtime.

---

## 6. Tests und Qualitätssicherung
- **Integrationstests:** REST-API mit Postman/Newman getestet.  
- **Functional Tests:** Browser-Smoketests mit Playwright (`npm run test:e2e` im `frontend/`-Verzeichnis).
- **Load Tests:** Separater Jenkins-Job mit k6, um Ressourcen zu schonen.
- **Monitoring:** Docker-Logs werden via `promtail` an Grafana Loki weitergeleitet; Dashboards werden beim Starten des `grafana`-Services aus `docker-compose.yml` automatisch provisioniert.

---

## 7. Rückschläge und Lessons Learned
1. **VM-Snapshots**
   - Mehrmals notwendig, da fehlerhafte Firewall- oder SSH-Configs den Zugriff blockierten.

2. **Infrastructure as Code**
   - Nach manuellen Versuchen: Wechsel zu Ansible-Playbooks für Wiederholbarkeit.

3. **Kommunikation**
   - Tägliche Stand-ups halfen beim schnellen Austausch.  
   - Entscheidungsprotokolle in Confluence dokumentiert.

---

## 8. Nächste Schritte
- Pipeline um Security-Scans (Snyk, Trivy) erweitern.  
- Terraform für automatisierte Staging-/QA-Umgebungen.  
- Jenkins-Backups automatisieren.

---

## 🧩 Fazit
Trotz anfänglicher Schwierigkeiten mit der VM und späteren Problemen in Jenkins steht nun eine funktionierende CI/CD-Landschaft.  
Durch klare Aufgabentrennung, konsequentes Troubleshooting und Automatisierungsschritte entstand ein stabiles Fundament für die Weiterentwicklung der WetterApp.

---

**Repository:** [https://github.com/MarioB06/weatherApp](https://github.com/MarioB06/weatherApp)  
**Abgabe:** Modul 324 – DevOps Introduction  
**Datum:** Oktober 2025
