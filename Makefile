NAME	:= leovm

SRC_DIR		:= vm/src
OBJ_DIR		:= build
SRCS		:= \
	main.cpp \
	vm.cpp \
	reader.cpp \
	int.cpp \
	float.cpp \
	bool.cpp

SRCS	:= $(SRCS:%=$(SRC_DIR)/%)
OBJS	:= $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

CC	:= g++
CFLAGS	:= -Wall -Wextra -Werror
CPPFLAGS	:= -I include
RM          := rm -f
MAKEFLAGS   += --no-print-directory
DIR_DUP     = mkdir -p $(@D)

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(OBJS) -o $(NAME)
	$(info CREATED $(NAME))

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(DIR_DUP)
	$(CC) $(CFLAGS) $(CPPFLAGS) -c -o $@ $<
	$(info CREATED $@)

clean:
	$(RM) $(OBJS)

fclean: clean
	$(RM) $(NAME)

re:
	$(MAKE) fclean
	$(MAKE) all


.PHONY: all clean fclean re
.SILENT:
