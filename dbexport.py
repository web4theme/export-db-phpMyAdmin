import requests
import re
import datetime
import traceback
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for insecure requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_token_from_html(html_content):
    """
    Extracts the token from the HTML content using regex.
    
    Args:
        html_content (str): The HTML content to search for the token.
    
    Returns:
        str: The extracted token, or None if not found.
    """
    token_match = re.search(r'name="token" value="([^"]+)"', html_content)
    if token_match:
        return token_match.group(1)
    return None

def download_database(username, password):
    """
    Downloads a database backup from a phpMyAdmin instance.
    
    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    session = requests.Session()

    try:
        print("Accessing the page to retrieve the token...")
        response = session.get(
            'https://web4theme.com/phpmyadmin',
            headers=headers,
            auth=(username, password),
            verify=False
        )
        
        if response.status_code == 200:
            token = get_token_from_html(response.text)
            if not token:
                print("Failed to retrieve the token from the page.")
                return
                
            print(f"Successfully retrieved token: {token}")

            # List of table names (requires manual addition)
            tables = [
                'wp_actionscheduler_actions', 'wp_actionscheduler_claims', 'wp_actionscheduler_groups'
            ]

            # Initialize the data dictionary
            data = {
                'db': 'dbname1',
                'token': token,
                'export_type': 'database',
                'export_method': 'quick',
                'template_id': '',
                'quick_or_custom': 'quick',
                'what': 'sql',
                'structure_or_data_forced': '0',
                'table_select[]': [],    # Use a list to store multiple values
                'table_structure[]': [], # Use a list to store multiple values
                'table_data[]': [],     # Use a list to store multiple values
                'aliases_new': '',
                'output_format': 'sendit',
                'filename_template': '@DATABASE@',
                'remember_template': 'on',
                'charset': 'utf-8',
                'compression': 'none',
                'maxsize': '',
                'sql_include_comments': 'something',
                'sql_header_comment': '',
                'sql_use_transaction': 'something',
                'sql_compatibility': 'NONE',
                'sql_structure_or_data': 'structure_and_data',
                'sql_create_table': 'something',
                'sql_auto_increment': 'something',
                'sql_create_view': 'something',
                'sql_procedure_function': 'something',
                'sql_create_trigger': 'something',
                'sql_backquotes': 'something',
                'sql_type': 'INSERT',
                'sql_insert_syntax': 'both',
                'sql_max_query_size': '50000',
                'sql_hex_for_binary': 'something',
                'sql_utc_time': 'something'
            }

            # Add table names to the corresponding lists
            for table in tables:
                data['table_select[]'].append(table)
                data['table_structure[]'].append(table)
                data['table_data[]'].append(table)

            print("Starting database backup download...")
            response = session.post(
                'https://web4theme.com/phpmyadmin/export.php',
                headers=headers,
                auth=(username, password),
                data=data,
                verify=False,
                stream=True
            )
            
            if response.status_code == 200:
                current_date = datetime.datetime.now().strftime("%Y%m%d")
                filename = f"backup_dbname_{current_date}.sql"
                
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
                print(f"Database backup successfully saved to: {filename}")
            else:
                print(f"Download failed, status code: {response.status_code}")
                print("Response content:")
                print(response.text)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(traceback.format_exc())
    
    finally:
        session.close()

if __name__ == "__main__":
    username = "loginusername"
    password = "pwd"
    download_database(username, password)
