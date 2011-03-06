#!/bin/bash

echo -n "Generating openldap2-client "

cp openldap2.spec openldap2-client.spec
cp openldap2.changes openldap2-client.changes

perl -pi -e "s/^Name:.*openldap2$/Name:         openldap2-client/g"  openldap2-client.spec

echo "Done."

