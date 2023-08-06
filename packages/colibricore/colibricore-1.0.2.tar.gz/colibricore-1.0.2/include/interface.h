#ifndef COLIBRIINTERFACE_H
#define COLIBRIINTERFACE_H

/**
 * @file interface.h
 * \brief Abstract interfaces.
 *
 * @author Maarten van Gompel (proycon) <proycon@anaproy.nl>
 * 
 * @section LICENSE
 * Licensed under GPLv3
 *
 * @section DESCRIPTION
 * Abstract interfaces
 */

/**
 * Limited interface to pattern stores
 */
class PatternStoreInterface {
    public:
        /**
         * Does the pattern occur in the pattern store?
         */
        virtual bool has(const Pattern &) const =0;
        /**
         * Does the pattern occur in the pattern store?
         */
        virtual bool has(const PatternPointer &) const =0;
        /**
         * How many patterns are in the pattern store?
         */
        virtual size_t size() const =0; 
};

/**
 * Basic read-only interface for pattern models, abstract base class.
 */
class PatternModelInterface: public PatternStoreInterface {
    public:
        /**
         * Get the type of the model
         * @return ModelType
         */
        virtual int getmodeltype() const=0;

        /**
         * Get the version number of the model
         */
        virtual int getmodelversion() const=0;
        
        //these are already in PatternStoreInterface:
            //virtual bool has(const Pattern &) const =0;
            //virtual bool has(const PatternPointer &) const =0;
            //virtual size_t size() const =0; 

        /**
         * Returns the number of times this pattern occurs in the model
         */
        virtual unsigned int occurrencecount(const Pattern & pattern)=0;

        /**
         * Returns the number of times the frequency of the pattern in the
         * model, a relative/normalised value
         */
        virtual double frequency(const Pattern &) =0;

        /**
         * Return the maximum pattern length in this model
         */
        virtual int maxlength() const=0;
        /**
         * Returns the minumum pattern length in this model
         */
        virtual int minlength() const=0;

        /**
         * Return the number of distinct words/unigram in the original corpus,
         * includes types not covered by the model!
         */
        virtual unsigned int types() =0;

        /**
         * Returns the number of tokens in the original corpus, includes tokens
         * not covered by the model!
         */
        virtual unsigned int tokens() const=0;

        virtual PatternStoreInterface * getstoreinterface() {
            return (PatternStoreInterface*) this;
        };
};

#endif
