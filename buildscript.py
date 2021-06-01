from subprocess import run
from uuid import uuid4
from os import makedirs

DOCKERFILE = r'''
FROM maven:3-openjdk-11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/andreaphylum/hbase-connectors .
CMD ["mvn", "package", "-DskipTests"]
'''

if __name__ == '__main__':
    file_list = [
        'hbase-connectors-assembly/target/hbase-connectors-1.0.1-SNAPSHOT-jar-with-dependencies.jar',
        'spark/hbase-spark/target/hbase-spark-1.0.1-SNAPSHOT.jar',
        'spark/hbase-spark-it/target/hbase-spark-it-1.0.1-SNAPSHOT.jar',
        'spark/hbase-spark-protocol/target/hbase-spark-protocol-1.0.1-SNAPSHOT-sources.jar',
        'spark/hbase-spark-protocol/target/hbase-spark-protocol-1.0.1-SNAPSHOT.jar',
        'spark/hbase-spark-protocol-shaded/target/hbase-spark-protocol-shaded-1.0.1-SNAPSHOT-sources.jar',
        'spark/hbase-spark-protocol-shaded/target/hbase-spark-protocol-shaded-1.0.1-SNAPSHOT.jar',
        'spark/hbase-spark-protocol-shaded/target/original-hbase-spark-protocol-shaded-1.0.1-SNAPSHOT.jar',
    ]
    container_name = f'hbase-connector-builder-{uuid4()}'
    run('docker build -f - -t hbase-connector-builder .'.split(),
        input=DOCKERFILE.encode('utf-8'))
    run(f'docker run -it --name {container_name} hbase-connector-builder')
    makedirs('LIB', exist_ok=True)
    for filename in file_list:
        run(f'docker container cp {container_name}:/opt/hbase-connectors/{filename} LIB')
    run(f'docker rm {container_name}')
