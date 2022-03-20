/*******************************************************************************************
*
*   raylib [core] example - Basic window (adapted for HTML5 platform)
*
*   This example is prepared to compile for PLATFORM_WEB, PLATFORM_DESKTOP and PLATFORM_RPI
*   As you will notice, code structure is slightly diferent to the other examples...
*   To compile it for PLATFORM_WEB just uncomment #define PLATFORM_WEB at beginning
*
*   This example has been created using raylib 1.3 (www.raylib.com)
*   raylib is licensed under an unmodified zlib/libpng license (View raylib.h for details)
*
*   Copyright (c) 2015 Ramon Santamaria (@raysan5)
*
********************************************************************************************/

#include "raylib.h"

//#define PLATFORM_WEB

#if defined(PLATFORM_WEB)
    #include <emscripten/emscripten.h>
#endif


#include <mruby.h>
#include <mruby/compile.h>
#include <mruby/string.h>
#include <mruby/class.h>
#include <mruby/data.h>
#include <mruby/numeric.h>
#include <mruby/string.h>
#include <mruby/presym.h>
#include <mruby/compile.h>
#include <mruby/dump.h>
#include <mruby/proc.h>

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>






static void
printstr(mrb_state *mrb, const char *p, mrb_int len)
{
    fwrite(p, (size_t)len, 1, stdout);
  fflush(stdout);
}

static mrb_value
mrb_printstr(mrb_state *mrb, mrb_value self)
{
  mrb_value s = mrb_get_arg1(mrb);

  if (mrb_string_p(s)) {
    printstr(mrb, RSTRING_PTR(s), RSTRING_LEN(s));
  }
  return s;
}


static mrb_value mrb_print(mrb_state *mrb, mrb_value self)
{
  mrb_int argc, i;
  const mrb_value *argv;
  mrb_get_args(mrb, "*", &argv, &argc);
  for (i=0; i<argc; i++) {
    mrb_value s = mrb_obj_as_string(mrb, argv[i]);
    printstr(mrb, RSTRING_PTR(s), RSTRING_LEN(s));
  }
  return mrb_nil_value();
}


static mrb_value mrb_puts(mrb_state *mrb, mrb_value self)
{
  mrb_int argc, i;
  const mrb_value *argv;

  mrb_get_args(mrb, "*", &argv, &argc);
  for (i=0; i<argc; i++) {
    mrb_value s = mrb_obj_as_string(mrb, argv[i]);
    mrb_int len = RSTRING_LEN(s);
    printstr(mrb, RSTRING_PTR(s), len);
    if (len == 0 || RSTRING_PTR(s)[len-1] != '\n') {
      printstr(mrb, "\n", 1);
    }
  }
  if (argc == 0) {
    printstr(mrb, "\n", 1);
  }
  return mrb_nil_value();
}


static mrb_value
execute_file(mrb_state *mrb, const char* input)
{
  mrbc_context *c;
  mrb_value result;

  FILE *infile;


  c = mrbc_context_new(mrb);
 //c->dump_result = TRUE;

  if ((infile = fopen(input, "r")) == NULL)
  {
      fprintf(stderr, " cannot open program file. (%s)\n",  input);
      return mrb_nil_value();

  }
  mrbc_filename(mrb, c, input);
 //  mrb_load_irep_file(mrb,infile);
   result = mrb_load_irep_file_cxt(mrb, infile, c);

  fclose(infile);
  mrbc_context_free(mrb, c);

    if (mrb->exc)
    {
      if (!mrb_undef_p(result))
      {
        mrb_print_error(mrb);
      }
     return mrb_nil_value();
    }
    else
    {
      printf("Syntax OK \n");
    }
  /*
  if (mrb_undef_p(result))
  {
    return mrb_nil_value();
  }*/
  return result;
}

static mrb_value mrb_GetTickCount(mrb_state *mrb, mrb_value self)
{

  //return mrb_fixnum_value(GetTickCountMs());
  return mrb_float_value(mrb,GetTime());

}



void
mrb_mruby_print_gem_init(mrb_state* mrb)
{
  struct RClass *krn;
  krn = mrb->kernel_module;
  mrb_define_method(mrb, krn, "__printstr__", mrb_printstr, MRB_ARGS_REQ(1));
  mrb_define_method(mrb, krn, "print", mrb_print, MRB_ARGS_ANY());
  mrb_define_method(mrb, krn, "puts", mrb_puts, MRB_ARGS_ANY());
  mrb_define_method(mrb, krn, "getTickCount", mrb_GetTickCount, MRB_ARGS_NONE());
}

void
mrb_mruby_print_gem_final(mrb_state* mrb)
{
}

//----------------------------------------------------------------------------------
// Global Variables Definition
//----------------------------------------------------------------------------------
int screenWidth = 800;
int screenHeight = 450;

//----------------------------------------------------------------------------------
// Module Functions Declaration
//----------------------------------------------------------------------------------
void UpdateDrawFrame(void);     // Update and Draw one frame

//----------------------------------------------------------------------------------
// Main Enry Point
//----------------------------------------------------------------------------------
int main()
{



  mrb_state *mrb = mrb_open();
  if (!mrb) {  }

  mrb_show_copyright(mrb);
  mrb_show_version(mrb);
  mrb_mruby_print_gem_init(mrb);
//  mrb_value v = mrb_load_string(mrb, "puts 'hello world'");

    mrbc_context *c;
    c = mrbc_context_new(mrb);

  //  mrb_value v = mrb_load_string_cxt(mrb, "puts 'hello world'", NULL);


 mrb_value v= execute_file(mrb,"resources/save.mrb");


    // Initialization
    //--------------------------------------------------------------------------------------
    InitWindow(screenWidth, screenHeight, "raylib [core] example - basic window");






#if defined(PLATFORM_WEB)
    emscripten_set_main_loop(UpdateDrawFrame, 0, 1);
#else
    SetTargetFPS(60);   // Set our game to run at 60 frames-per-second
    //--------------------------------------------------------------------------------------

    // Main game loop
    while (!WindowShouldClose())    // Detect window close button or ESC key
    {
        UpdateDrawFrame();
    }
#endif

    // De-Initialization
    //--------------------------------------------------------------------------------------
    CloseWindow();        // Close window and OpenGL context
    //--------------------------------------------------------------------------------------



  mrbc_context_free(mrb, c);
  mrb_close(mrb);

    return 0;
}

//----------------------------------------------------------------------------------
// Module Functions Definition
//----------------------------------------------------------------------------------
void UpdateDrawFrame(void)
{
    // Update
    //----------------------------------------------------------------------------------
    // TODO: Update your variables here
    //----------------------------------------------------------------------------------

    // Draw
    //----------------------------------------------------------------------------------
    BeginDrawing();

        ClearBackground(RAYWHITE);

        DrawText("Congrats! ruby in android!", 190, 200, 20, LIGHTGRAY);

    EndDrawing();
    //----------------------------------------------------------------------------------
}