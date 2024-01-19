/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Library for the Draco encoding/decoding feature inside the glTF-Blender-IO project.
 *
 * The python script within glTF-Blender-IO uses the CTypes library to open the DLL,
 * load function pointers add pass the raw data to the encoder.
 *
 * @author Jim Eckerlein <eckerlein@ux3d.io>
 * @date   2020-11-18
 */

#pragma once

#include "common.h"

struct Encoder;

Encoder* encoderCreate(uint32_t vertexCount);

void encoderRelease(Encoder *encoder);

void encoderSetCompressionLevel(Encoder* encoder, uint32_t compressionLevel);

void encoderSetQuantizationBits(Encoder* encoder, uint32_t position, uint32_t normal, uint32_t uv, uint32_t color, uint32_t generic);

bool encoderEncode(Encoder* encoder, uint8_t preserveTriangleOrder);

uint64_t encoderGetByteLength(Encoder* encoder);

void encoderCopy(Encoder*encoder, uint8_t* data);

void encoderSetIndices(Encoder* encoder, size_t indexComponentType, uint32_t indexCount, void* indices);

uint32_t encoderSetAttribute(Encoder* encoder, char* attributeName, size_t componentType, char* dataType, void* data);

uint32_t encoderGetEncodedVertexCount(Encoder* encoder);

uint32_t encoderGetEncodedIndexCount(Encoder* encoder);
