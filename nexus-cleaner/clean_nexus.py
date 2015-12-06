#!/usr/bin/python3

import sys
import argparse
import xml.etree.ElementTree as xml_parser
import requests

def get_arguments(cli_args):
    """
    Defines command line arguments
    :return: command line parameters with values
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', required=True)
    parser.add_argument('--repo-id', required=True)
    parser.add_argument('--group-id', required=True)
    parser.add_argument('--delete-versions', required=True)
    parser.add_argument('--keep-versions', required=False)
    parser.add_argument('--dry-run', action='store_true', required=False)
    return parser.parse_args(cli_args)

def main():
    """
    Cleans up a nexus repository
    """
    arguments = get_arguments(sys.argv[1:])
    versions_to_keep = []
    resources = []

    if arguments.keep_versions:
        versions_to_keep = arguments.keep_versions.rsplit(",")

    artifact_uris = find_resource_uris(arguments.endpoint + "/nexus/service/local/repositories/"
                                       + arguments.repo_id + "/content/" + arguments.group_id.replace(".", "/"))
    for artifact_uri in artifact_uris:
        resources += find_resource_uris(artifact_uri)

    deleted_resources = 0;
    for resource in resources:
        version = resource.rsplit("/")[-2]
        if version_in_range(version, arguments.delete_versions) and version not in versions_to_keep:
            if not arguments.dry_run:
                delete_resource(resource)
                deleted_resources += 1
                print(resource + " has been deleted")
            else:
                print(resource + " would have been deleted if not in dry-run mode")
        else:
            print(resource + " has been kept")

    if deleted_resources > 0:
        print("Rebuilding maven metadata...")
        delete_resource(arguments.endpoint + "/nexus/service/local/metadata/repositories/" + arguments.repo_id + "/content/")

def version_in_range(version, range):
    range = range.rsplit("-")
    min = tuple(range[0].rsplit("."))
    max = tuple(range[1].rsplit("."))
    version = tuple(version.rsplit("."))
    if min < version < max:
        return True
    else:
        return False

def find_resource_uris(url):
    uri_list = []
    response = requests.get(url)
    xml_root = xml_parser.fromstring(response.text)
    uris = xml_root.findall('.//resourceURI')
    for uri in uris:
        # ignore maven-metadata files
        if uri.text.endswith('/'):
            uri_list.append(uri.text)
    return uri_list

def delete_resource(url):
    response = requests.delete(url)
    if not response.status_code == requests.codes.no_content:
        print("WARNING: Attempt to delete " + url + " returned unexpected status code: " + response.status_code)

if __name__ == '__main__':
    main()