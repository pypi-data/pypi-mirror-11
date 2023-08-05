/*
* Copyright @ CERN, 2015.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*    http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

#ifndef LOGGINGHELPER_H
#define LOGGINGHELPER_H

#include <gfal_api.h>

namespace PyGfal2 {

/**
 * Makes the use of the Python logging facilities easier
 */
void logging_helper(const gchar *log_domain, GLogLevelFlags log_level,
        const gchar *message, gpointer user_data);

};

#endif // LOGGINGHELPER_H
