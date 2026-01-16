# Use OpenJDK 17 base image
FROM openjdk:17-jdk-slim

# Set working directory inside the container
WORKDIR /app

# Copy the Maven pom.xml file
COPY pom.xml .

# Copy the source code
COPY src ./src

# Build the application using Maven
RUN ./mvnw clean package -DskipTests

# Expose port 8080
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "target/user-management-0.0.1-SNAPSHOT.jar"]