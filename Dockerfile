FROM python:3.10

WORKDIR /scrapyApp

# Copy your application code
COPY . /scrapyApp

# Copy Scrapyd configuration
COPY scrapyd.conf /etc/scrapyd/scrapyd.conf

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install Google Chrome (if needed)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || true && \
    apt-get update && apt-get -f install -y && \
    echo "Chrome: " && google-chrome --version

# Install Scrapyd
RUN pip install scrapyd

# Expose Scrapyd port
EXPOSE 6800

# Start Scrapyd
CMD scrapyd & sleep 5 && scrapyd-deploy default && tail -f /dev/null