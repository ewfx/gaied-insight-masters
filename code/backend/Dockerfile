# Use the official Python 3.11.5 image
FROM python:3.11.5

# Set the working directory
WORKDIR /app

# Copy the backend folder into the container
COPY backend /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI runs on
EXPOSE 7860

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
