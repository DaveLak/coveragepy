# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Simple value objects for tracking what to do with files."""

from __future__ import annotations

from typing import Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from coverage.plugin import FileTracer


class FileDisposition:
    """A simple value type for recording what to do with a file."""

    original_filename: str
    canonical_filename: str
    source_filename: Optional[str]
    trace: bool
    reason: str
    file_tracer: Optional[FileTracer]
    has_dynamic_filename: bool

    def __repr__(self) -> str:
        return f"<FileDisposition {self.canonical_filename!r}: trace={self.trace}>"


# FileDisposition "methods": FileDisposition is a pure value object, so it can
# be implemented in either C or Python.  Acting on them is done with these
# functions.

def disposition_init(cls: Type[FileDisposition], original_filename: str) -> FileDisposition:
    """Construct and initialize a new FileDisposition object."""
    disp = cls()
    disp.original_filename = original_filename
    disp.canonical_filename = original_filename
    disp.source_filename = None
    disp.trace = False
    disp.reason = ""
    disp.file_tracer = None
    disp.has_dynamic_filename = False
    return disp


def disposition_debug_msg(disp: FileDisposition) -> str:
    """Make a nice debug message of what the FileDisposition is doing."""
    if disp.trace:
        msg = f"Tracing {disp.original_filename!r}"
        if disp.original_filename != disp.source_filename:
            msg += f" as {disp.source_filename!r}"
        if disp.file_tracer:
            msg += f": will be traced by {disp.file_tracer!r}"
    else:
        msg = f"Not tracing {disp.original_filename!r}: {disp.reason}"
    return msg
