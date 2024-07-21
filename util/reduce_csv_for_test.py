import pandas as pd

def reduce_csv_to_first_10_rows(input_file_path, output_file_path):
    df = pd.read_csv(input_file_path)    
    df_first_10_rows = df.head(10)

    df_first_10_rows.to_csv(output_file_path, index=False)
    print(f"Reduced file saved to {output_file_path}")

if __name__ == "__main__":
    resumes_input_file = 'data/input/resumes.csv'
    postings_input_file = 'data/input/postings.csv'

    resumes_post_edit_input_file = 'data/output/resumes_post_edit.csv'
    resumes_post_edit_output_file = 'data/output/reduced_resumes_post_edit.csv'

    resumes_output_file = 'data/output/reduced_resumes.csv'
    postings_output_file = 'data/output/reduced_postings.csv'

    reduce_csv_to_first_10_rows(resumes_input_file, resumes_output_file)
    reduce_csv_to_first_10_rows(resumes_post_edit_input_file, resumes_post_edit_output_file)
    reduce_csv_to_first_10_rows(postings_input_file, postings_output_file)
