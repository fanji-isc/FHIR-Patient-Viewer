# Use the official InterSystems IRIS for Health Community Edition image
FROM containers.intersystems.com/intersystems/irishealth-community:latest-em

# Switch to the root user to perform administrative tasks
USER root

# Create necessary directories for scripts, configuration, and data storage
RUN mkdir -p /scripts \
 && mkdir -p /data/ifconfig \
 && mkdir -p /fhirdata

# Copy FHIR data set into the container
COPY ./fhirdata/100Set /fhirdata/

# Copy configuration merge file for InterSystems IRIS
COPY ./merge/CMF.cpf /merge/CMF.cpf

# Set correct ownership of directories for the IRIS user and group
RUN chown -R ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /data/ \
 && chown -R ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /fhirdata/ \
 && chown -R ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /merge/

# Copy necessary scripts for configuring the FHIR server
COPY ./scripts/fhirserver.script /scripts/fhirserver.script
COPY ./scripts/enablecors.script /scripts/enablecors.script

# Ensure scripts have the correct ownership
RUN chown -R ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /scripts/

# Switch to the IRIS user for security best practices
USER ${ISC_PACKAGE_MGRUSER}

# Start IRIS, execute the FHIR server setup script, and then stop IRIS
RUN iris start IRIS && \
    iris session IRIS < /scripts/fhirserver.script && \
    iris session IRIS < /scripts/enablecors.script && \
    iris stop IRIS quietly

# Expose the necessary ports
EXPOSE 52773 1972

# Set environment variables for IRIS configuration
ENV ISC_DATA_DIRECTORY=/data/ifconfig
ENV ISC_CPF_MERGE_FILE=/merge/CMF.cpf

# Define the entrypoint to execute when the container starts
ENTRYPOINT [ "/iris-main" ]
