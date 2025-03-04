async def resolve_channel_ids(client, channel_data_list):
    """
    Converts channel usernames into entity IDs.
    """
    resolved_channels = []
    for channel_data in channel_data_list:
        try:
            # Attempt to resolve the channel ID for the provided URL
            print(f"Trying to resolve channel ID: {channel_data['url']}")
            entity = await client.get_entity(channel_data['url'])
            resolved_channels.append((entity, channel_data))  # Store the entity and channel data
            print(f"Channel found: {entity.title}")
        except Exception as e:
            # Handle any errors that occur while trying to resolve the channel
            print(f"Error resolving channel {channel_data['url']}: {e}")
            continue
        
    return resolved_channels
