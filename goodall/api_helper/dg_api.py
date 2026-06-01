from pprl_data_generator_service_api_client import (
    GermanyGeneratorConfig,
    UsvrSelectionConfig, TaggedDatasetDto, RecordCluster,
)

from goodall.api_helper.pprl_clients import Service, get_client
import pprl_data_generator_service_api_client as dg

client = get_client(Service.Data_generator)
generator_controller = dg.DataGeneratorApi(client)
selector_controller = dg.DataSelectorApi(client)


def generate_dataset(
    number_of_records: int, include_household_structures: bool
) -> TaggedDatasetDto:
    request = GermanyGeneratorConfig(
        numberOfRecords=number_of_records,
        includeHouseholdStructures=include_household_structures,
    )
    return generator_controller.generate(request)


def select_dataset(
    num_records_a: int, num_records_b: int, num_duplicates: int, seed: str
):
    request = UsvrSelectionConfig.from_dict(
        {
            "clusterType": "nc",
            "numRecordsA": num_records_a,
            "numRecordsB": num_records_b,
            "numDuplicates": num_duplicates,
            "attributeColumns": [
                "FIRSTNAME",
                "MIDDLEAME",
                "LASTNAME",
                "YEAROFBIRTH",
                "CITY",
                "PLZ",
            ],
            "orderingStrategy": "SEEDED_SHUFFLE",
            "orderingSeed": seed,
            "changeFilter": {
                "minChanges": 1,
                "changedAttributes": [
                    "FIRSTNAME",
                    "MIDDLEAME",
                    "LASTNAME",
                    "CITY",
                    "PLZ",
                ],
            },
        }
    )
    return selector_controller.select(request)

def get_clusters(
    type: str, num_clusters: int, orderingStrategy: str = "SEEDED_SHUFFLE", seed: str = "abcd"
) -> list[RecordCluster]:
    request = UsvrSelectionConfig(
        clusterType=type,
        numClusters=num_clusters,
        orderingStrategy=orderingStrategy,
        orderingSeed=seed
    )
    return selector_controller.retrieve_clusters(request)
