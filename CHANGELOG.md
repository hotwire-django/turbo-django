# Turbo-Django Changelog

0.4.2 - 2022-05-13
    * Removes duplicate and incorrect render method from UserBroadcastComponent.

0.4.1 - 2022-05-13
    * Moves correct render() method to BaseComponent

0.4.0 - 2022-05-12
    * Adds Turbo Components, easy to add turbo-frames with an associated stream and template.

0.3.0 - 2021-12-05
    * Stream class added to explicitly declare streams
    * Streams auto-detected in streams.py
    * TurboMixin has been removed. ModelStreams replace this functionality with linked model declared in Meta.model
    * Permissions can now be written by overriding the Stream.user_passes_test() method
    * Support for stream-less turbo-frame responses to POST requests

0.2.5 - 2021-12-05
    * Update Turbo library to 7.1.0
