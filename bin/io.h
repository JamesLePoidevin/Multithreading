#ifndef H_ED_IO_20030121102334
#define H_ED_IO_20030121102334

/* ---------------------------------------------------------------------
   io.h

   1.0 : 12-11-2003 : intial version
   1.1 : 13-11-2004 : [f]get_d() added
   1.2 : 12-02-2005 : [f]get_line() added (dynamic)
   --------------------------------------------------------------------- */

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdio.h>
#include "ed/inc/types.h"

/* macros ============================================================== */
/* constants =========================================================== */

   enum
   {
      IO_OK,
      IO_ERR_READ,
      IO_ERR_LENGTH,
      IO_ERR_BUFFER,
      IO_ERR_CONVERSION,
      IO_ERR_EMPTY,
      IO_ERR_OUTPUT_ADDRESS,
      IO_ERR_FILE,
      IO_ERR_BUFFER_SIZE,
      IO_ERR_NB
   };

/* types =============================================================== */
/* structures ========================================================== */
/* internal public data ================================================ */
/* internal public functions =========================================== */
/* entry points ======================================================== */

   char const *io_sver (void);
   char const *io_sid (void);

   int fget_s (char *s, size_t size, FILE * fp);
   int fget_c (FILE * fp);
   int fget_l (long *p, FILE * fp);
   int fget_ul (ulong * p, FILE * fp);
   int fget_d (double *p, FILE * fp);

   int get_s (char *s, size_t size);
   int get_c (void);
   int get_l (long *p);
   int get_ul (ulong * p);
   int get_d (double * p);

   /* Dynamic. To be freed */
   char *fget_line (FILE * fp, int *p_end);
   /* lit une ligne dans le fichier fp ouvert en lecture texte
      si p_end vauf NULL, il est ignore (peu recommande)
      sinon, il prend la valeur 1 en fin de lecture, sinon il est inchange.
   */
   char *get_line (void);

   void io_perror (int err);

/* public data ========================================================= */

#ifdef __cplusplus
}
#endif

#endif                          /* H_ED_IO_20030121102334 */
/* GUARD (c) ED 2000-2002 Dec 16 2002 Ver. 1.4 */
