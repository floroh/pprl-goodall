from pprl_protocol_manager_service_api_client import DatasetCsvDto

from goodall.api_helper.pm_api import add_data_owner_dataset

dataset_id_to_path_mapping = {
    2010: "NCVR_10_10_1_min1E_n00",
    2012: "NCVR_10_10_2_min1E_n00",
    2032: "NCVR_50_50_10_min1E_n00",
}

if __name__ == "__main__":
    dataset_ids = [2010, 2012, 2032]
    for dataset_id in dataset_ids:
        print("Importing dataset {}".format(dataset_id))
        add_data_owner_dataset(DatasetCsvDto(
            dataset_id=dataset_id,
            path=f"data/datasets/{dataset_id_to_path_mapping[dataset_id]}",
        ))