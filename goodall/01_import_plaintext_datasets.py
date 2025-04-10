from pprl_protocol_manager_service_api_client import DatasetCsvDto

from goodall.api_helper.pm_api import add_data_owner_dataset

dataset_id_to_path_mapping = {
    2010: "NCVR_10_10_1_min1E_n00",
    2012: "NCVR_10_10_2_min1E_n00",
    2014: "NCVR_10_10_3_min1E_n00",
    2030: "NCVR_50_50_5_min1E_n00",
    2032: "NCVR_50_50_10_min1E_n00",
    2034: "NCVR_50_50_15_min1E_n00",
    2040: "NCVR_50_50_5_min2E_n00",
    2042: "NCVR_50_50_10_min2E_n00",
    2044: "NCVR_50_50_15_min2E_n00",
}

if __name__ == "__main__":
    dataset_ids = [2030, 2032, 2034, 2040, 2042]
    # for dataset_id in dataset_id_to_path_mapping.keys():
    for dataset_id in dataset_ids:
        print("Importing dataset {}".format(dataset_id))
        add_data_owner_dataset(DatasetCsvDto(
            dataset_id=dataset_id,
            path=f"/datasets/{dataset_id_to_path_mapping[dataset_id]}",
        ))