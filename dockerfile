# Gunakan base image PHP dengan Apache
FROM php:8.1-apache

# Install ekstensi PHP yang diperlukan
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Copy semua file proyek ke dalam container
COPY . /var/www/html/

# Atur hak akses
RUN chown -R www-data:www-data /var/www/html

# Expose port 80
EXPOSE 80

# Jalankan Apache
CMD ["apache2-foreground"]
