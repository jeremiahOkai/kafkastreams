#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status

# Create Kafka topics
/opt/kafka/bin/kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --create --topic weather-data --partitions 2 --replication-factor 2 &&
    /opt/kafka/bin/kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --create --topic weather-transformed --partitions 2 --replication-factor 2 &&
    /opt/kafka/bin/kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --create --topic user-data --partitions 2 --replication-factor 2 &&
    /opt/kafka/bin/kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --create --topic user-transformed --partitions 2 --replication-factor 2 &&
    /opt/kafka/bin/kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --create --topic test-topic --partitions 2 --replication-factor 2
