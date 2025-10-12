# Erfahrungsbericht: Infrastruktur-Aufbau von Marc und Luan

Diese Zusatzdokumentation beschreibt im Detail, wie wir – Marc und Luan – die Infrastruktur für das WetterApp-Projekt aufgebaut haben. Wir erläutern unsere Herangehensweise, die wichtigsten Meilensteine sowie die größten Stolpersteine (vor allem rund um die VM- und Jenkins-Konfiguration).

## 1. Projektstart und Zielsetzung
- **Ziel**: Eine CI/CD-Pipeline für das WetterApp-Projekt einrichten, die Build, Tests und Deployment automatisiert.
- **Teamaufteilung**: Marc kümmerte sich vorrangig um die Infrastruktur (VM, Netzwerke, Sicherheit), während Luan die Pipeline-Schritte in Jenkins und Docker optimierte. Entscheidungen wurden gemeinsam getroffen.

## 2. Vorbereitung der virtuellen Maschine
1. **VM-Auswahl**
   - Wir entschieden uns für eine Ubuntu-Server-VM in unserer Private-Cloud.
   - Wichtige Spezifikationen: 4 vCPUs, 8 GB RAM, 100 GB SSD.
2. **Erste Stolpersteine**
   - Das vorinstallierte Image war veraltet, wodurch `apt update` regelmäßig fehlschlug.
   - Lösung: Neues Cloud-Image beziehen und alle Pakete direkt nach dem ersten Boot aktualisieren (`apt update && apt upgrade`).
3. **Netzwerk & Zugriff**
   - SSH-Zugriff war zunächst blockiert, weil die Standard-Sicherheitsgruppe nur internen Traffic erlaubte.
   - Marc hat die Firewall-Regeln angepasst (Port 22/tcp freigegeben) und Fail2ban aktiviert, um Brute-Force-Angriffe zu verhindern.
4. **Nutzer- und Rechteverwaltung**
   - Gemeinsamer Benutzer `ci-admin` angelegt.
   - SSH-Keys von Marc und Luan hinterlegt, Passwort-Login deaktiviert.

## 3. Basis-Setup auf der VM
1. **Systempakete**
   - Installation von Docker, Docker Compose und Git.
   - Problem: Der Docker-Dienst startete nach einem Reboot nicht automatisch.
   - Lösung: `systemctl enable docker` und Service-Logs prüfen (`journalctl -u docker`).
2. **Python- und Node-Umgebung**
   - Für Backend (Python) und Frontend (Node) wurden getrennte Umgebungen vorbereitet.
   - Luan hat `pyenv` und `nvm` eingerichtet, damit sich Tool-Versionen sauber verwalten lassen.
3. **Monitoring & Logging**
   - `htop`, `iotop` und `docker stats` installiert, um Engpässe schnell zu erkennen.
   - Zusätzliche SSH-Logins werden via `journalctl -u ssh` überwacht.

## 4. Jenkins-Installation und -Konfiguration
1. **Installationsprobleme**
   - Bei der ersten Installation fehlten Java-Abhängigkeiten (`OpenJDK 11`).
   - Lösung: `apt install openjdk-11-jdk` vor dem Jenkins-Debian-Paket.
2. **Jenkins als Dienst**
   - Nach dem Setup startete Jenkins, brach aber nach einigen Minuten mit Speicherfehlern ab.
   - Ursache: Standard `JAVA_OPTS` nicht ausreichend (nur 256 MB Heap).
   - Lösung: `JAVA_OPTS="-Xms512m -Xmx2048m"` in `/etc/default/jenkins` ergänzt.
3. **Reverse Proxy & TLS**
   - Wir haben Nginx vorgeschaltet, um Jenkins über HTTPS erreichbar zu machen.
   - Let’s-Encrypt-Zertifikate via `certbot` eingerichtet.
4. **Benutzer- und Rechteverwaltung**
   - Marc erstellte ein dediziertes Jenkins-Admin-Konto, Luan verwaltete Projektrollen.
   - Matrix-basierte Sicherheit aktiviert, sodass nur unser Team Pipeline-Konfigurationen anpassen darf.

## 5. Pipeline-Aufbau
1. **Repository-Anbindung**
   - Jenkins wurde mit GitHub Webhooks verbunden.
   - Stolperstein: Webhook-Requests wurden vom Proxy blockiert (fehlende Weiterleitung des `X-Forwarded-Proto`-Headers).
   - Lösung: Nginx-Konfiguration angepasst und Jenkins neu gestartet.
2. **Build-Stufen**
   - **Backend**: Python-Tests via `pytest` und statische Analyse mit `flake8`.
   - **Frontend**: `npm install`, `npm run build` und `npm run test`.
   - **Docker**: Multi-stage Builds; Images werden ins interne Registry gepusht.
3. **Credentials-Handling**
   - Secrets (Registry-Token, GitHub PAT) im Jenkins-Credentials-Store hinterlegt.
   - Luan erstellte Ordner-spezifische Credentials und Parameter für die Pipeline.
4. **Automatisiertes Deployment**
   - Erfolgreiche Builds lösen ein `docker-compose pull` & `docker-compose up -d` auf der Produktions-VM aus.
   - Rolling-Restarts sichern kurze Downtime.

## 6. Tests und Qualitätssicherung
- Jenkins-Stage für Integrationstests der REST-API (Postman/Newman).
- Browser-basierte Smoke-Tests via Playwright.
- Lasttest (k6) im separaten Jenkins-Job, da ressourcenintensiv.
- Monitoring: Alerts aus Docker-Logs werden via `promtail` nach Grafana Loki weitergeleitet.

## 7. Rückschläge und Lessons Learned
1. **VM Snapshots sind Gold wert**
   - Mehrfach musste auf einen Snapshot zurückgesprungen werden, weil Konfigurationsänderungen den SSH-Zugriff blockierten.
2. **Infrastructure as Code**
   - Nach ersten manuellen Schritten haben wir die VM-Konfiguration in Ansible-Playbooks gegossen, um Wiederholbarkeit zu sichern.
3. **Transparente Kommunikation**
   - Tägliche Stand-ups halfen, Probleme schnell zu eskalieren.
   - Entscheidungslogbuch geführt (Confluence), um nachzuvollziehen, warum wir bestimmte Tools gewählt haben.

## 8. Nächste Schritte
- Pipeline um Security-Scans (Snyk, Trivy) erweitern.
- Terraform-basierte Bereitstellung weiterer Umgebungen (Staging, QA).
- Automatisierte Backups der Jenkins-Konfiguration.

---

**Fazit**: Trotz der anfänglichen Probleme mit VM-Zugriff und Jenkins-Konfiguration steht nun eine robuste CI/CD-Landschaft. Durch klare Aufgabenteilung, konsequentes Troubleshooting und wiederholbare Automatisierungsschritte konnten wir ein stabiles Fundament für die Weiterentwicklung der WetterApp schaffen.
