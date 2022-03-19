def to_subscribable_name(stream_name):
    return stream_name.__str__().replace(":", ".")
