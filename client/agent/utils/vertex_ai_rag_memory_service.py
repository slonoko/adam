from __future__ import annotations

from collections import OrderedDict
import json
import os
import tempfile
from typing import Optional
from typing import TYPE_CHECKING

from google.genai import types
from typing_extensions import override
from google.adk.memory.vertex_ai_rag_memory_service import VertexAiRagMemoryService
from google.adk.sessions import Session
from dotenv import load_dotenv
import vertexai
import os

load_dotenv()

vertexai.init(location=os.getenv("GOOGLE_CLOUD_LOCATION"))

class FixedVertexAiRagMemoryService(VertexAiRagMemoryService):

  @override
  async def add_session_to_memory(self, session: Session):
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json"
    ) as temp_file:

      output_lines = []
      for event in session.events:
        if not event.content or not event.content.parts:
          continue
        text_parts = [
            part.text.replace("\n", " ")
            for part in event.content.parts
            if part.text
        ]
        if text_parts:
          output_lines.append(
              {
                  "author": event.author,
                  "timestamp": event.timestamp,
                  "text": ".".join(text_parts),
              }
          )
      output_string = json.dumps(output_lines)
      temp_file.write(output_string)
      temp_file_path = temp_file.name
    if not self._vertex_rag_store.rag_resources:
      raise ValueError("Rag resources must be set.")

    from google.adk.dependencies.vertexai import rag

    for rag_resource in self._vertex_rag_store.rag_resources:
      rag.upload_file(
          corpus_name= rag_resource.rag_corpus,
          path=temp_file_path,
          # this is the temp workaround as upload file does not support
          # adding metadata, thus use display_name to store the session info.
          display_name=f"{session.app_name}.{session.user_id}.{session.id}",
      )

    os.remove(temp_file_path)