from loguru import logger

from pprl_data_owner_service_api_client import (
    EncodingIdDto,
    MultiRecordEncodingRetrievalRequestDto,
    RecordDto,
    EncodingRequestDto,
)

from goodall.api_helper.pprl_clients import Service, get_client
import pprl_data_owner_service_api_client as do

client = get_client(Service.Data_owner_1)
dataset_controller = do.DatasetManagementApi(client)
config_controller = do.ConfigurationManagementApi(client)
encoder_controller = do.EncoderApi(client)
on_the_fly_encoder_controller = do.OnTheFlyEncoderApi(client)
corrupter_controller = do.CorrupterApi(client)


def get_records(dataset_id: int, limit: int = -1) -> list[RecordDto]:
    logger.debug(f"Getting records for dataset {dataset_id} with limit {limit}")
    if limit >= 0:
        return dataset_controller.get_all(dataset_id=dataset_id, limit=limit)
    return dataset_controller.get_all(dataset_id=dataset_id)


def get_config(method: str) -> do.EncodingDto:
    return config_controller.get_encoding(
        encoding_id_dto=do.EncodingIdDto(method=method)
    )

def encode(
    record: RecordDto, method: str, project: str = "exampleProject"
) -> RecordDto:
    return on_the_fly_encoder_controller.encode1(
        EncodingRequestDto(
            encodingId=EncodingIdDto(method=method, project=project), record=record
        )
    )


def fetch_encoded_dataset(
    dataset_id: int, method: str, project: str = "exampleProject"
):
    request = MultiRecordEncodingRetrievalRequestDto.from_dict(
        {
            "encodingId": EncodingIdDto.from_dict(
                {"method": method, "project": project}
            ),
            "datasetId": dataset_id,
        }
    )
    return encoder_controller.encode_multiple_same(request)
