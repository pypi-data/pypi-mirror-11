#!/bin/bash
set -e

function lookup_for_objects() {
    set +e

    echo -n "Looking for image $IMAGE_NAME ... "
    export img_id=$(nova $INSECURE image-list | grep " $IMAGE_NAME " | awk '{print $2}')
    if [ ! -z "$img_id" ] ; then
        echo " Found"
    else
        echo " Not Found"
    fi

    echo -n "Looking for flavor $FLAVOR_NAME ... "
    export flavor_id=$(nova $INSECURE flavor-list | grep " $FLAVOR_NAME " | awk '{print $2}')
    if [ ! -z "$flavor_id" ] ; then
        echo " Found"
    else
        echo " Not Found"
    fi

    groups_ids=""
    export missed_groups=""
    for SERV_GROUP in $SERV_GROUPS ; do
        echo -n "Looking for server-group $SERV_GROUP ... "
        group_id=$(nova $INSECURE server-group-list | grep " $SERV_GROUP " | awk '{print $2}' )
        if [ ! -z "$group_id" ] ; then
            echo " Found"
            export groups_ids="$groups_ids $group_id"
        else
            echo " Not Found"
            export missed_groups="$missed_groups $SERV_GROUP"
        fi
    done

    if [ ! -z "$KEYPAIR_NAME" ] ; then
        echo -n "Looking for keypair $KEYPAIR_NAME ... "
        export keypair_id=$(nova $INSECURE keypair-list | grep " $KEYPAIR_NAME " | awk '{print $2}' )
        if [ ! -z "$keypair_id" ] ; then
            echo " Found"
        else
            echo " Not Found"
        fi
    fi

    echo -n "Looking for security group $SECGROUP ... "
    export secgroup_id=$(nova $INSECURE secgroup-list | grep " $SECGROUP " | awk '{print $2}' )
    if [ ! -z "$secgroup_id" ] ; then
        echo " Found"
    else
        echo " Not Found"
    fi

    set -e
}

function clean() {
    lookup_for_objects

    if [ ! -z "$img_id" ] ; then
        echo "Deleting $IMAGE_NAME image"
        nova $INSECURE image-delete "$img_id" >/dev/null
    fi

    if [ ! -z "$flavor_id" ] ; then
        echo "Deleting $FLAVOR_NAME flavor"
        nova $INSECURE flavor-delete "$flavor_id" >/dev/null
    fi

    for group_id in $groups_ids ; do
        echo "Deleting server-group $SERV_GROUP"
        nova $INSECURE server-group-delete "$group_id" >/dev/null
    done

    if [ ! -z "$keypair_id" ] ; then
        echo "deleting keypair $KEYPAIR_NAME"
        nova $INSECURE keypair-delete "$KEYPAIR_NAME" >/dev/null
    fi

    if [ -f "$KEY_FILE_NAME" ] ; then
        echo "deleting keypair file $KEY_FILE_NAME"
        rm -f "$KEY_FILE_NAME"
    fi

    if [ ! -z "$secgroup_id" ] ; then
        nova $INSECURE secgroup-delete $SECGROUP >/dev/null
    fi
}

function prepare() {
    if [ "$OS_INSECURE" -eq "1" ] ; then
        export INSECURE="--insecure"
    fi

    lookup_for_objects

    if [ -z "$img_id" ] ; then
        echo "Creating $IMAGE_NAME  image"

        # opts="--disk-format qcow2 --container-format bare --is-public true"
        # glance $INSECURE image-create --name "$IMAGE_NAME" $opts --copy-from "$IMAGE_URL" >/dev/null

        IMAGE_FILE="/tmp/${IMAGE_NAME}.qcow"
        if [ ! -f "$IMAGE_FILE" ] ; then
            curl "$IMAGE_URL" -o "$IMAGE_FILE" 2>&1 >/dev/null
        fi
        opts="--disk-format qcow2 --container-format bare --is-public true"
        glance $INSECURE image-create --name "$IMAGE_NAME" $opts --file "$IMAGE_FILE" >/dev/null
        echo "Image created, but may need a time to became active"
    fi

    if [ -z "$flavor_id" ] ; then
        echo "Creating flavor $FLAVOR_NAME"
        nova $INSECURE flavor-create "$FLAVOR_NAME" "$FLAVOR_NAME" "$FLAVOR_RAM" "$FLAVOR_HDD" "$FLAVOR_CPU_COUNT" >/dev/null
    fi

    for SERV_GROUP in $missed_groups ; do
        echo "Creating server group $SERV_GROUP"
        nova $INSECURE server-group-create --policy anti-affinity "$SERV_GROUP" >/dev/null
        group_id=$(nova $INSECURE server-group-list | grep " $SERV_GROUP " | awk '{print $2}' )
        export groups_ids="$groups_ids $group_id"
    done

    if [ ! -z "$KEYPAIR_NAME" ] ; then
        if [ -z "$keypair_id" ] ; then
            echo "Creating server group $SERV_GROUP. Key would be stored into $KEY_FILE_NAME"
            nova $INSECURE keypair-add "$KEYPAIR_NAME" > "$KEY_FILE_NAME"
            chmod og= "$KEY_FILE_NAME"
        fi
    fi

    if [ -z "$secgroup_id" ] ; then
        echo "Adding rules for ping and ssh"
        nova $INSECURE secgroup-create $SECGROUP $SECGROUP >/dev/null
        nova $INSECURE secgroup-add-rule $SECGROUP icmp -1 -1 0.0.0.0/0 >/dev/null
        nova $INSECURE secgroup-add-rule $SECGROUP tcp 22 22 0.0.0.0/0 >/dev/null
    fi
}

if [ "$1" = "--clear" ] ; then
    clean
else
    prepare
fi
