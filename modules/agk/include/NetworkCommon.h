#ifndef _H_NETWORK_COMMON
#define _H_NETWORK_COMMON

	#include "PlatformDefines.h"

	#ifdef AGK_WINDOWS
		#include "WindowsNetwork.h"
	#endif


	#ifdef AGK_ANDROID
		#include "AndroidNetwork.h"
	#endif


	#ifdef AGK_LINUX
		#include "LinuxNetwork.h"
	#endif

	
	#ifdef AGK_HTML5
		#include "HTML5Network.h"
	#endif

#endif
