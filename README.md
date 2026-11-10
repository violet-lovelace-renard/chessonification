# Chessonification

Making music, algorithmically, from a chess game

## Design

> Which musical composition problems are you trying to solve?

Melody, harmony, instrumentation, rhythm?

all of them! we want to solve the problem of making bangers (beautiful music) with chess drivers :)

> What CS models would you like to explore?

Genetic, grammars, Markov, neural networks?

> What algorithmic approaches interest you?

Deterministic vs. stochastic, sorting vs. searching?

> What real-world phenomena can inspire your work?

Chess. (onification)

## Spitballing zone

* Pawns as percussion
  * Start with 8
  * Instrument changes w/ position
* Each piece as own instrument
  * Pawns = drum set? + timpani or something?
  * Rooks = bass/trumpet/brass?
  * Bishops = flute/basson
  * Knight = violin? cello (not those horrible violas)
  * Queen = vocal (operatic?) / Hammond organ?
  * King = triangle?? (that's percussion but uh sure)
  maybe modulation/key?
* What dictates pitches?
  * Maybe we take from music mouse and use the row and column pos to determine pitch? would we want pieces to play 2 pitches or one pitch?
  * incorperate the tile that the piece is coming from as well
  * row is o, column is pitch name?
* Sonifying other events
  * Attacks/tactics
  (perhaps when a capture event happens a four bar battle sequence happens)
  * Promotion
  * Castling
  * Check, stale/checkmate
  * En passant (lol)
* Switching between White + Black?
  * In terms of "whose" instruments are being played?
  * Differences between White + Black instruments, stylistically
    * e.g., upright vs. electric bass
  * Eval bar??? (dominance determined by who is winning at the time)
* What are the file formats for chess games?
  * PGN
  * Loading in games
  * Live
