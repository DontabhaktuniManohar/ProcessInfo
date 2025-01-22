[ABCD]
APP=/app
LOG=/log
DEFAULT_APP_COUNT=1

[ABCD_ServerGroups]
group1=abc.company.com,def.company.com
group1_app_count=2
group2=ghi.company.com,jkl.company.com
group2_app_count=3

[DEFG]
APP=/app
LOG=/log
DEFAULT_APP_COUNT=1

[DEFG_ServerGroups]
group1=mno.company.com,pqr.company.com
group1_app_count=2
group2=stu.company.com,vwx.company.com
group2_app_count=4

############
import configparser

def get_app_count_for_servers(config_file, section_prefix, servers):
    # Load the configuration file
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Initialize the server-to-APP_COUNT dictionary
    server_app_counts = {}
    
    # Iterate through sections to find matching groups
    for section in config.sections():
        if section.startswith(section_prefix):
            if 'DEFAULT_APP_COUNT' in config[section_prefix]:
                default_app_count = int(config[section_prefix]['DEFAULT_APP_COUNT'])
            else:
                default_app_count = 1  # Fallback default

            # Read server groups and their app counts
            for key, value in config[section].items():
                if key.endswith('_app_count'):
                    continue
                app_count_key = f"{key}_app_count"
                app_count = int(config[section].get(app_count_key, default_app_count))
                for server in value.split(','):
                    server_app_counts[server.strip()] = app_count

    # Assign app counts for requested servers
    return {
        server: server_app_counts.get(server, default_app_count) for server in servers
    }

# Example usage
if __name__ == "__main__":
    config_file = 'appdetails.cfg'
    section_prefix = 'ABCD'  # Change this dynamically for different sections
    servers = ['abc.company.com', 'def.company.com', 'ghi.company.com', 'mno.company.com']
    
    app_counts = get_app_count_for_servers(config_file, section_prefix, servers)
    for server, count in app_counts.items():
        print(f"Server: {server}, APP_COUNT: {count}")
