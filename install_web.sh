cp -R web/ /var/www/html/
chown -R www-data:www-data /var/www/html/web/
sed -i 's/welcome/web/' /var/www/html/FullPageDashboard/urls.json
