FROM ubuntu:16.04
 RUN mkdir -p /home/se/.aws/ \
     groupadd -r appuser && useradd -r -g appuser appuser \
     chown -R appuser:appuser /var/www /var/log/apache2 /etc/apache2
 COPY awssecret.json /home/se/.aws/credentials
 RUN apt-get update && \
     apt-get install -y apache2=2.4.18-2ubuntu3.17
 USER appuser
 EXPOSE 80
 HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
   CMD curl -f http://localhost/ || exit 1
 CMD ["apache2ctl", "-D", "FOREGROUND"]
